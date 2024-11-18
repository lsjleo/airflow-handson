import os
import configparser
import shutil
from jupyterhub.spawner import LocalProcessSpawner
from oauthenticator.google import LocalGoogleOAuthenticator

c = get_config()
c.Application.show_config = False
c.Application.show_config_json = False
c.JupyterHub.active_server_limit = 6
c.JupyterHub.active_user_window = 1800
c.JupyterHub.activity_resolution = 30
c.JupyterHub.admin_access = True

c.JupyterHub.authenticator_class = LocalGoogleOAuthenticator
c.LocalGoogleOAuthenticator.oauth_callback_url = os.getenv('GOOGLE_OAUTH_CALLBACK')
c.LocalGoogleOAuthenticator.client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
c.LocalGoogleOAuthenticator.client_secret = os.getenv('GOOGLE_OAUTH_SECRET_ID')
c.Authenticator.add_user_cmd = ['adduser', '-q', '--gecos', '""', '--disabled-password', '--force-badname']
c.LocalGoogleOAuthenticator.create_system_users = True
c.LocalGoogleOAuthenticator.hosted_domain = os.getenv('GOOGLE_OAUTH_DOMAIN')
c.LocalGoogleOAuthenticator.login_service = os.getenv('GOOGLE_OAUTH_SERVICE')

c.JupyterHub.cookie_max_age_days = 7
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 9088
c.JupyterHub.init_spawners_timeout = 1200
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 9000
c.JupyterHub.redirect_to_server = True
c.JupyterHub.show_config = False
c.JupyterHub.show_config_json = False
c.JupyterHub.shutdown_on_logout = True
c.Spawner.cmd = ["jupyter-labhub"]
c.Spawner.cpu_guarantee = 0.5
c.Spawner.cpu_limit = 2
c.Spawner.http_timeout = 1200
c.Authenticator.admin_users = {'admin','leonardo.jeronimo'}
c.Authenticator.auth_refresh_age = 300
c.Authenticator.manage_groups = True
c.JupyterHub.ssl_key = '/home/jupyter/jupyter.key'
c.JupyterHub.ssl_cert = '/home/jupyter/jupyter.crt'
c.LocalAuthenticator.create_system_users = True
c.JupyterLabTemplates.template_dirs = ['/home/jupyter/templates']
c.JupyterLabTemplates.include_default = True
c.JupyterLabTemplates.include_core_paths = True

class SnowparkFormSpawner(LocalProcessSpawner):
    def _options_form_default(self):
        username = self.user.name
        self.user.name = username
        
        default_env = "YOURNAME=%s\n" % username
        awsenv = "aws_access_key_id=\naws_secret_access_key="
        snsenv = "SNOWFLAKE_USER=\nSNOWFLAKE_PASS=\nSNOWFLAKE_ROLE=\nSNOWFLAKE_WAREHOUSE=\nSNOWFLAKE_ACCOUNT=dob24868.us-east-1"
        
        form =  """
        <div class="form-group">
            <label for="env">ENV VARS</label>
            <textarea class="form-control" name="env">{env}</textarea>
        </div>
        """.format(env=default_env)
        
        if not os.path.exists(f'/home/{username}/.snowflake'):    
            form += """
            <div class="form-group">
                <label for="env">SNOWFLAKE CREDENTIALS</label>
                <textarea class="form-control" name="snsenv">{snsenv}</textarea>
            </div>
            """.format(snsenv=snsenv)
            
        if not os.path.exists(f'/home/{username}/.aws'):    
            form += """
            <div class="form-group">
                <label for="env">AWS CREDENTIALS</label>
                <textarea class="form-control" name="awsenv">{awsenv}</textarea>
            </div>
            """.format(awsenv=awsenv)
        
        return form

    def options_from_form(self, formdata):
        username = self.user.name
        options = {}
        options['env'] = env = {}

        env_lines = formdata.get('env', [''])
        for line in env_lines[0].splitlines():
            if line:
                key, value = line.split('=', 1)
                env[key.strip()] = value.strip()
                
        sn_lines = formdata.get('snsenv', [''])
        sncontent = configparser.ConfigParser()
        sncontent.add_section('credentials')
        for line in sn_lines[0].splitlines():
            if line:
                key, value = line.split('=', 1)  
                sncontent['credentials'][key] = value
        if not os.path.exists(f'/home/{username}/.snowflake'):
            os.makedirs(f'/home/{username}/.snowflake')
            with open(f'/home/{username}/.snowflake/snowflake.config', 'w') as fb:
                sncontent.write(fb)
            
        aws_lines = formdata.get('awsenv', [''])
        awscontent = configparser.ConfigParser()
        awscontent.add_section('default')
        for line in aws_lines[0].splitlines():
            if line:
                key, value = line.split('=', 1)  
                awscontent['default'][key] = value
        if not os.path.exists(f'/home/{username}/.aws'):
            os.makedirs(f'/home/{username}/.aws')
            with open(f'/home/{username}/.aws/credentials', 'w') as fb:
                awscontent.write(fb)
                
        if not os.path.exists(f'/home/{username}/.ssh'):
            os.makedirs(f'/home/{username}/.ssh')
            os.system(f'openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out /home/{username}/.ssh/rsa_key.p8 -nocrypt')
            os.system(f'openssl rsa -in /home/{username}/.ssh/rsa_key.p8 -pubout -out /home/{username}/.ssh/rsa_key.pub')
            os.system(f"echo \nSNOWFLAKE_TOKEN=$(cat /home/{username}/.ssh/rsa_key.pub | tail -n +2 | head -n -1 | tr -d '\n') >> /home/{username}/.snowflake/snowflake.config")
            
        return options

    def get_env(self):
        env = super().get_env()
        if self.user_options.get('env'):
            env.update(self.user_options['env'])
        return env


c.JupyterHub.spawner_class = SnowparkFormSpawner
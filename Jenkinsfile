pipeline {

  agent {
    // Node setup : minimal centos7, plugged into Jenkins, and
    // git config --global http.sslVerify false
    // sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
    // sudo yum -y install python36u python36u-pip python36u-devel git curl gcc
    // git config --global http.sslVerify false
    // sudo curl -fsSL get.docker.com | bash
    label 'Molecule_Slave'
  }

  stages {

    stage ('Get latest code') {
      steps {
        checkout scm
      }
    }

    stage('SonarQube analysis') {
      environment {
        scannerHome = tool 'SonarQube-3.3.0.1492'
      }
      steps {
        withSonarQubeEnv('SysMango SonarQube') {
          sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=vault-service -Dsonar.sources=. -Dsonar.login=e0f0e320aa71842559f7998dfd2af26cf1848f3f"
        }
      }
    }

    stage ('Setup Python virtual environment') {
      steps {
        sh '''
          export HTTP_PROXY=http://10.123.123.123:8080
          export HTTPS_PROXY=http://10.123.123.123:8080
          pip3.6 install virtualenv
          virtualenv virtenv
          source virtenv/bin/activate
          pip install --upgrade ansible molecule docker
        '''
      }
    }

    stage ('Display versions') {
      steps {
        sh '''
          source virtenv/bin/activate
          docker -v
          python -V
          ansible --version
          molecule --version
        '''
      }
    }

    stage ('Molecule test') {
      steps {
        sh '''
          source virtenv/bin/activate
          molecule test
        '''
      }
    }

    stage('Create archive and upload') {
      steps{
        zip archive: true, dir: '', glob: '', zipFile: 'vault-service.zip'
        nexusArtifactUploader(
          nexusVersion: 'nexus3',
          protocol: 'http',
          nexusUrl: 'nexus.sysmango.net',
          groupId: 'production',
          version: '1.0.0.$BUILD_NUMBER',
          repository: 'ansible',
          credentialsId: 'nexus-creds',
          artifacts: [
              [artifactId: 'vault-service',
               classifier: '',
               file: 'vault-service.zip',
               type: 'zip']
          ]
        )
        nexusArtifactUploader(
          nexusVersion: 'nexus3',
          protocol: 'http',
          nexusUrl: 'nexus.sysmango.net',
          groupId: 'production',
          version: 'latest',
          repository: 'ansible',
          credentialsId: 'nexus-creds',
          artifacts: [
            [artifactId: 'vault-service',
            classifier: '',
            file: 'vault-service.zip',
            type: 'zip']
          ]
        )
      }
    }
  }
}

}

pipeline {
  agent any
  environment {
    DEB_PACKAGE_DIR = 'hello-world-deb'
    ARTIFACTORY_URL = 'https://taii217.jfrog.io/artifactory'
    ARTIFACTORY_REPO = 'hello-world-debian'
    ARTIFACTORY_USER = 'nguyenducphattai217@gmail.com'
    ARTIFACTORY_API_KEY = credentials('artifactory-access-token')
    PATH = "/path/to/dpkg-deb:$PATH"
  }

    stages {
      stage('prepare') {
        steps{
          script {
            sh '''
              sudo -S apt-get update
              sudo -S apt-get install dpkg
            '''
          }
        }
      }
      stage('Build Debian Package') {
        steps {
          script {
            sh "dpkg-deb --build ${DEB_PACKAGE_DIR}"
          }
        }
      }
      stage('Deploy to Artifactory') {
        steps {
          script {
            def packageName = sh(script: "ls *.deb | awk -F/ '{print \$NF}'", returnStdout: true).trim()
            // Artifactory deployment configuration
            def buildInfo = Artifactory.newBuildInfo()
      
            artifactoryUpload(
              serverId: 'hello-world-debian',
              spec: """{
                  "files": [
                      {
                          "pattern": "path/to/your/artifacts/*",
                          "target": "${ARTIFACTORY_REPO}/",
                          "props": "build.name=${BUILD_TAG};build.number=${BUILD_NUMBER}"
                      }
                  ]
              }""",
              buildInfo: buildInfo
            )
          }
        }
      }
    }

    post {
        success {
            echo 'Debian package successfully built and deployed to Artifactory.'
        }
    }
}

pipeline {
  agent any
  environment {
    DEB_PACKAGE_DIR = 'hello-world-deb'
    ARTIFACTORY_URL = 'https://taii217.jfrog.io/artifactory'
    ARTIFACTORY_REPO = 'hello-world-debian'
    ARTIFACTORY_USER = 'nguyenducphattai217@gmail.com'
    SERVER_ID = 'taii217.jfrog.io'
    ARTIFACTORY_API_KEY = credentials('artifactory-access-token')
    BUILD_NAME = 'debian-macos'
    PATH = "/opt/homebrew/bin:$PATH"
  }

    stages {
      stage('Build Debian Package') {
        steps {
          script {
            bat "dpkg-deb --build ${DEB_PACKAGE_DIR}"
          }
        }
      }
      stage('Upload Build Info and Artifact to Artifactory') {
        steps {
          script {
              rtPublishBuildInfo (
                  serverId: SERVER_ID,
                  buildName: BUILD_NAME,
                  buildNumber: BUILD_NUMBER
              )
          }
        }
      }
      stage('Deploy to Artifactory') {
        steps {
          script {
            def packageName = bat(script: "ls *.deb | awk -F/ '{print \$NF}'", returnStdout: true).trim()
            // Artifactory deployment configuration
      
            rtUpload(
              serverId: SERVER_ID,
              spec: """{
                  "files": [
                      {
                          "pattern": "*.deb",
                          "target": "${ARTIFACTORY_REPO}/",
                          "props": "build.name=${BUILD_TAG};build.number=${BUILD_NUMBER}"
                      }
                  ]
              }""",
              buildName: BUILD_NAME,
              buildNumber: BUILD_NUMBER
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

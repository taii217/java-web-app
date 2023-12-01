pipeline {
  agent any

  options {
      buildDiscarder(logRotator(numToKeepStr: '5'))
  }

  environment {
      BUILD_NAME = "safeview_ami_bake"
      BUILD_NUMBER = "${BUILD_NUMBER}"
      ARTIFACTORY_USER = 'admin'
      ARTIFACTORY_API_KEY = credentials('artifactory-access-token')
      SERVER_ID = 'taii217.jfrog.com'
      ARTIFACTORY_URL = "https://taii217.jfrog.io"
  }

  stages {
      stage('Show Build Info') {
          steps {
              script {
                  echo "Build Info: ${BUILD_NAME}#${BUILD_NUMBER}"
              }
          }
      }

      stage('Upload Build Info and Artifact to Artifactory') {
          steps {
              script {
                  def server = Artifactory.server ARTIFACTORY_URL, ARTIFACTORY_USER, ARTIFACTORY_API_KEY
                  def buildInfo = Artifactory.newBuildInfo()

                  buildInfo.env.capture = true
                  buildInfo.name = BUILD_NAME
                  buildInfo.number = BUILD_NUMBER

                  server.publishBuildInfo buildInfo
              }
          }
      }
  }
}
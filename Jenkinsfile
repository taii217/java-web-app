pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
  environment {
      BUILD_INFO = "safeview_ami_bake#${BUILD_NUMBER}"
      ARTIFACTORY_API_KEY  = credentials('artifactory-access-token')
      SERVER_ID = 'taii217.menloinfra.com'
      ARTIFACTORY_URL = "https://taii217.jfrog.io"
  }
  stages {
    // stage('Build') {
    //   steps {
    //     sh './mvnw clean install'
    //   }
    // }
    stage('show') {
      steps {
        echo "${BUILD_INFO}"
      }
    }
    stage('Upload Build Info and Artifact to Artifactory') {
      steps {
        script {
          def server = Artifactory.server ARTIFACTORY_URL, ARTsIFACTORY_USER, ARTIFACTORY_API_KEY
          def buildInfo = Artifactory.newBuildInfo()

          buildInfo.env.capture = true
          buildInfo.name = BUILD_NAME
          buildInfo.number = BUILD_NUMBER

          rtPublishBuildInfo (
            serverId: server_id,
            buildName: build_name,
            buildNumber: build_number,
          )
        }
      }
    }
  }
}

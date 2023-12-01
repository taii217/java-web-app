pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }

    environment {
        BUILD_NAME = "safeview_ami_bake"
        BUILD_NUMBER = "${BUILD_NUMBER}"
        ARTIFACTORY_USER = 'nguyenducphattai217@gmail.com'
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
                    rtPublishBuildInfo (
                        serverId: SERVER_ID,
                        buildName: BUILD_NAME,
                        buildNumber: BUILD_NUMBER,
                        modules: [Artifactory.newModuleInfo()]
                    )
                }
            }
        }
    }
}

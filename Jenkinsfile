pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }

    environment {
        BUILD_NAME = "safeview_ami_bake"
        BUILD_NUMBER = "${BUILD_NUMBER}"
        ARTIFACTORY_API_KEY = credentials('artifactory-access-token')
        SERVER_ID = 'taii217.jfrog.io'
        ARTIFACTORY_URL = "https://taii217.jfrog.io"
    }

    stages {
        stage('Show Build Info') {
            steps {
                echo "Build Info: ${BUILD_NAME}#${BUILD_NUMBER}"
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
        // stage('Upload Build Info and Artifact to Artifactory 2') {
        //     steps {
        //         script {
        //             def buildInfo1 = Artifactory.newBuildInfo()
        //             buildInfo1.name = 'my-app-linux'
        //             buildInfo1.number = BUILD_NUMBER
        //             server.publishBuildInfo buildInfo1
        //         }
        //     }
        // }
    }
}

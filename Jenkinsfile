pipeline {
    agent any
    environment {
        DEB_PACKAGE_DIR = 'hello-world-deb'
        ARTIFACTORY_URL = 'https://taii217.jfrog.io/artifactory'
        ARTIFACTORY_REPO = 'hello-world-debian'
        SERVER_ID = 'taii217.jfrog.io'
        STACK_TAG = "hello_world"
        PATH = "/opt/homebrew/bin:$PATH"
    }
    stages {
        stage('Prepare') {
            steps {
                rtBuildInfo (
                    captureEnv: true, 
                    buildName: BUILD_TAG, 
                    buildNumber: BUILD_NUMBER,
                    startDate: new Date(currentBuild.startTimeInMillis)
                )
                sh 'env | sort'
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
                    // Artifactory deployment configuration
                    rtUpload(
                        serverId: SERVER_ID,
                        spec: """{
                            "files": [
                                {
                                    "pattern": "*.deb",
                                    "target": "${ARTIFACTORY_REPO}/${STACK_TAG}/${BUILD_NUMBER}/",
                                    "props": "build.name=${BUILD_TAG};build.number=${BUILD_NUMBER}"
                                }
                            ]
                        }""",
                        failNoOp: false,
                        buildName: BUILD_TAG,
                        buildNumber: BUILD_NUMBER
                    )
                }
            }
        }
    }
    post {
        always {
            script {
                rtPublishBuildInfo (
                    serverId: SERVER_ID,
                    buildName: BUILD_TAG,
                    buildNumber: BUILD_NUMBER
                )
            }
        }
        success {
            echo 'Debian package successfully built and deployed to Artifactory.'
        }
        cleanup {
            print "Cleaning up workspace directories"
            cleanWs deleteDirs: true
        }
    }
}

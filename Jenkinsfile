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
                    buildName: STACK_TAG, 
                    buildNumber: BUILD_NUMBER,
                    startDate: new Date(currentBuild.startTimeInMillis)
                )
                // sh 'env | sort'
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
                                    "props": "build.name=${STACK_TAG};build.number=${BUILD_NUMBER}"
                                }
                            ]
                        }""",
                        failNoOp: false,
                        buildName: STACK_TAG,
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
                    buildName: STACK_TAG,
                    buildNumber: BUILD_NUMBER
                )
                setProps()
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


def setProps () {
    def pattern  = "artifactory-build-info/${STACK_TAG}/${BUILD_NUMBER}-*.json"
    def props = "STACK_TAG=${STACK_TAG};BUILD_NUMBER=${BUILD_NUMBER};"

    rtSetProps (
        serverId: SERVER_ID,
        spec: "{\"files\":[{\"pattern\":\"${pattern}\",\"sortBy\":[\"created\"],\"sortOrder\":\"desc\",\"limit\":1}]}",
        props: props,
        failNoOp: true
    ) 
}
pipeline {
    agent any
    environment {
        DEB_PACKAGE_DIR_1 = 'hello-world-deb'
        DEB_PACKAGE_DIR_2 = 'hello-water'
        ARTIFACTORY_URL = 'https://taii217.jfrog.io/artifactory'
        ARTIFACTORY_REPO = 'libs-debian'
        SERVER_ID = 'taii217.jfrog.io'
        STACK_TAG = "my-debian"
        GLOBAL_BUILD_ID = "${BUILD_NUMBER}"
        PATH = "/opt/homebrew/bin:$PATH"
    }
    stages {
        stage('Prepare') {
            steps {
                rtBuildInfo (
                    captureEnv: true, 
                    buildName: STACK_TAG, 
                    buildNumber: GLOBAL_BUILD_ID,
                    startDate: new Date(currentBuild.startTimeInMillis)
                )
                // sh 'env | sort'
            }
        }
        stage('Build Debian Package') {
            steps {
                script {
                    sh '''
                        dpkg-deb --build ${DEB_PACKAGE_DIR_1}
                        version=$(dpkg-deb -f ${DEB_PACKAGE_DIR_1}.deb Version)
                        mv ${DEB_PACKAGE_DIR_1}.deb ${DEB_PACKAGE_DIR_1}_\$version.deb
                    '''
                    sh '''
                        dpkg-deb --build ${DEB_PACKAGE_DIR_2}
                        version=$(dpkg-deb -f ${DEB_PACKAGE_DIR_2}.deb Version)
                        mv ${DEB_PACKAGE_DIR_2}.deb ${DEB_PACKAGE_DIR_2}_\$version.deb
                    '''
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
                                    "target": "${ARTIFACTORY_REPO}/${STACK_TAG}/${GLOBAL_BUILD_ID}/"
                                }
                            ]
                        }""",
                        failNoOp: false,
                        buildName: STACK_TAG,
                        buildNumber: GLOBAL_BUILD_ID
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
                    buildNumber: GLOBAL_BUILD_ID
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
    def pattern  = "artifactory-build-info/${STACK_TAG}/${GLOBAL_BUILD_ID}-*.json"
    def props = "STACK_TAG=${STACK_TAG};GLOBAL_BUILD_ID=${GLOBAL_BUILD_ID};"

    rtSetProps (
        serverId: SERVER_ID,
        spec: "{\"files\":[{\"pattern\":\"${pattern}\",\"sortBy\":[\"created\"],\"sortOrder\":\"desc\",\"limit\":1}]}",
        props: props,
        failNoOp: true
    ) 
}
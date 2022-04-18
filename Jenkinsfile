#! /usr/bin/groovy
import com.anaplan.buildtools.jenkins_pipelines.ArcusBuildState
import com.anaplan.buildtools.jenkins_pipelines.ContainerTemplates

@Library('Anaplan_Pipeline')

// This global variable will be updated with the unique build version for this project early in the pipeline
def VERSION
def SAST_APPLICATION = "harness"
def BUILD_LABEL = "build.${UUID.randomUUID().toString()}"
def FEATURE = "cloudprovider"
def CERTS_DOCKERFILE = "certs/Dockerfile"
// replace hello with your servicename
// also change the value in Chart.yaml
def NAME = "harness-cloudprovider"
def CERTS_CONTAINER_NAME = "certs-init"
def ACCOUNT = "harness"

static Map python3() {
    return [
        name: "python3",
        image: "docker-develop.anaplan-np.net/docker-base-images/python3-poetry:0.0.2",
        securityContext: [
            runAsUser: 0
        ],
        tty: true,
        command: ["cat"]
    ]
}

def buildPods(){
    def containers = ContainerTemplates.dockerBuildContainers()
    def size = containers.size()

    // Because the stage where the docker image is
    // built is also building the go binary
    // we need to modify the template to have more
    // memory the build will fail
    for (def i = 0; i < size; i++){
        def container = containers.get(i)
        if (container.get("name").equals("docker")){
            container.resources =
                    [
                            limits: [ memory: "3Gi" ],
                            requests: [ memory: "3Gi" ]
                    ]
            containers[i] = container
        }
    }

    return pod(containers + [ContainerTemplates.helm()] + [python3()])
}

pipeline {
    agent {
        kubernetes {
            label "${BUILD_LABEL}-${NAME}"
            yaml buildPods()
        }
    }
    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(daysToKeepStr: '365'))
        timeout(time: 90, unit: 'MINUTES')
    }

    stages {
        stage('Initialise Build') {
            steps {
                arcusInit(projectName: "${NAME}", versionType: "PATCH", branch: env.BRANCH_NAME, org: "dig-common", repo: "${NAME}")
                          script {
                            currentBuild.displayName = "${env.VERSION}"
                       }
                }
        }
        stage('Build') {
            steps{

                dir('./src/harness-onboard-cloudprovider') {
                    withCredentials([usernamePassword(credentialsId: 'jenkins_git', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                    container('python3'){
                            
                            script{
                                    def repoKey = 'anaplan-blobs'
                                    zip zipFile: 'harness-onboard-cloudprovider.zip', archive: true, dir: '.'
                                    def spec = """ {
                                        "files": [
                                            { 
                                                "pattern": "harness-onboard-cloudprovider.zip",
                                                "target": "${repoKey}/cd-tools/${env.VERSION}/harness-onboard-cloudprovider.zip"
                                            }
                                        ]
                                    }"""
                                    ArcusBuildState.artifactory.uploadArtifact(spec)
                                }
                            
                        }
                    }
                }
            }
        }
    } 
  }

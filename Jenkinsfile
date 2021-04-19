#!groovy

library identifier: "jenkins-lib@develop"


node {
            // cleanup everything before running anything.
            deleteDir()
            // Passing in https_proxy for all steps.
            withEnv(['https_proxy=http://cloud-proxy:3128', ]) {
                stage('Checkout'){
                    // Get code from github.
                    checkout scm
                }
                stage("pre-commit hooks") {
                    pipelineHelper.preCommitHooks()
                }
            }
}

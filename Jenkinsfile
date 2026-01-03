pipeline {
  agent any

  options {
    timestamps()
  }

  // If you already configured GitHub webhooks, this will trigger on push.
  // For Multibranch Pipeline jobs, you can remove this block.
  triggers {
    githubPush()
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python venv') {
      steps {
        script {
          if (isUnix()) {
            sh '''
              python3 -m venv .venv
              . .venv/bin/activate
              python -m pip install --upgrade pip
              pip install -r requirements-dev.txt
            '''
          } else {
            bat '''
              rem Prefer Windows Python Launcher (py); fallback to python
              where py >nul 2>&1
              if %errorlevel%==0 (
                py -3 -m venv .venv
              ) else (
                python -m venv .venv
              )
              call .venv\\Scripts\\activate
              python -m pip install --upgrade pip
              pip install -r requirements-dev.txt
            '''
          }
        }
      }
    }

    stage('Unit tests (pytest)') {
      steps {
        script {
          if (isUnix()) {
            sh '''
              . .venv/bin/activate
              mkdir -p reports
              pytest -q --junitxml=reports/pytest-junit.xml
            '''
          } else {
            bat '''
              call .venv\\Scripts\\activate
              if not exist reports mkdir reports
              pytest -q --junitxml=reports\\pytest-junit.xml
            '''
          }
        }
      }
    }

    stage('System tests (Robot Framework)') {
      steps {
        script {
          if (isUnix()) {
            sh '''
              . .venv/bin/activate
              mkdir -p robot_reports
              robot -d robot_reports --xunit robot_reports/robot-xunit.xml robot
            '''
          } else {
            bat '''
              call .venv\\Scripts\\activate
              if not exist robot_reports mkdir robot_reports
              robot -d robot_reports --xunit robot_reports\\robot-xunit.xml robot
            '''
          }
        }
      }
    }
  }

  post {
    always {
      // Show test trend in Jenkins (works for both pytest + robot)
      junit testResults: 'reports/pytest-junit.xml,robot_reports/robot-xunit.xml', allowEmptyResults: true

      // Keep raw reports as build artifacts
      archiveArtifacts artifacts: 'reports/**,robot_reports/**', fingerprint: true

      // Publish Robot HTML (requires HTML Publisher plugin). If plugin is missing,
      // Jenkins will show a clear error; you can remove this block if needed.
      publishHTML(target: [
        allowMissing: true,
        alwaysLinkToLastBuild: true,
        keepAll: true,
        reportDir: 'robot_reports',
        reportFiles: 'report.html,log.html',
        reportName: 'Robot Framework Report'
      ])
    }
  }
}

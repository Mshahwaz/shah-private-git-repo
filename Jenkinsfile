pipeline {
  agent any
  environment {
    IMAGE="shahwaz131/shah-flaskapp"
    TAG="${env.BUILD_NUMBER}"
  }
  stages {
    /*stage('Checkout SCM') {
      steps {
        git branch: 'main', credentialsId: 'github-pat', 
        url: 'https://github.com/Mshahwaz/shah-private-git-repo.git'
      }
    }*/
    stage('Build') {
      steps {
        echo "Building image..."
        sh 'docker build -t "$IMAGE:$TAG" -t "$IMAGE:latest" .'
      }
    }
    stage('Push') {
      steps {
        echo "Pushing image..."
        withCredentials([usernamePassword(credentialsId: 'docker-tok', passwordVariable: 'docker_pass', usernameVariable: 'docker_user')]) {
        echo "Logging in to Docker Hub..."
        sh 'echo "$docker_pass" | docker login -u "$docker_user" --password-stdin'
        sh 'docker push "$IMAGE:$TAG"'
        sh 'docker push "$IMAGE:latest"'
    }
      }
    }
    stage('Deploy') {
      steps {
        echo "Deploying..."
        sh '''docker pull "$IMAGE:$TAG"
        docker rm -f shah-flaskapp || true
        docker run -d --name shah-flaskapp -p 5000:5000 "$IMAGE:$TAG"'''
        sh '''
        cat > deploy-info-$BUILD_NUMBER.txt <<EOF
        build: $BUILD_NUMBER
        image: $IMAGE:$TAG
        commit: ${GIT_COMMIT}
        branch: $GIT_BRANCH
        time: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
        url: $BUILD_URL
        EOF'''
        archiveArtifacts artifacts: "deploy-info-${BUILD_NUMBER}.txt", fingerprint: true
      }
    }
    stage('Test') {
      steps {
        sh '''sleep 2
        echo "Hit http://localhost:5000 to see the app."'''
      }
    }
    stage('Cleanup') {
      steps {
        cleanWs()
      }
    }
  }
  post {
  success { 
    echo "Build ${env.BUILD_NUMBER} succeeded" 
    }
  failure { 
    echo "Build ${env.BUILD_NUMBER} failed" 
    }
  always { 
    echo "Build ${env.BUILD_NUMBER} finished" 
    }
  }
}

pipeline {
  agent any
  environment {
    IMAGE="shahwaz131/shah-flaskapp"
    TAG="${env.BUILD_NUMBER}"
  }
  stages {
    stage('Checkout SCM') {
      steps {
        git branch: 'main', credentialsId: 'github-pat', 
        url: 'https://github.com/Mshahwaz/shah-private-git-repo.git'
      }
    }
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
}

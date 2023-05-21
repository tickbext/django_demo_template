pipeline{
	agent none
	stage("tests"){
		agent{
			docker{
				image 'python:3.10'			
			}		
		}
		steps{
		sh '''
			pwd	
			python -m venve .venv
			. .venv/bin/activate
			pip install -r requirements.txt
			python manage.py test
		'''	
		}
	}

	stage("build"){
		agents any
		steps{
			sh 'docker build . -t tickbext/django_demo_template:${GIT_COMMIT} -t tickbext/django_demo_template:latest'
		}
	}

	stage("push"){
		agent any
		steps{
			withCredentials([usernamePassword(credentialsId: 'dockerCreds', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')])
			sh 'docker login -u ${USERNAME} -p ${PASSWORD}'
			sh 'docker push tickbext/django_demo_template:${GIT_COMMIT}'
			sh 'docker push tickbext/django_demo_template:latest'		
		
		}
	}
	
	stage("deploy") {
    agent any
    steps {
        withCredentials([sshUserPrivateKey(credentialsId: 'deploy_server', keyFileVariable: 'KEY_FILE')]) {
            sh 'ssh -o StrictHostKeyChecking=no -i ${KEY_FILE} ${USERNAME}@io12.me mkdir -p ~${WORKSPACE}'
            sh 'scp -o StrictHostKeyChecking=no -i ${KEY_FILE} docker-compose.yaml ${USERNAME}@server_ip:~${WORKSPACE}'
            sh 'ssh -o StrictHostKeyChecking=no -i ${KEY_FILE} ${USERNAME}@io12.me docker-compose -f ~${WORKSPACE}/docker-compose.yaml pull'
            sh 'ssh -o StrictHostKeyChecking=no -i ${KEY_FILE} ${USERNAME}@io12.me docker-compose -f ~${WORKSPACE}/docker-compose.yaml up -d'
        }
    }
}
}

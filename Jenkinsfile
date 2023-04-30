```
  pipeline{
        agent{
            docker{ image 'python:3.10'}
        }
        stages{
            stage('task'){
                steps{
                    sh '''
                        python -m venv .venv
                        . .venv/bin/activate
                        pip install -r requirements.txt
                        python3 manage.py test
                        '''
                }
            }
        }
}

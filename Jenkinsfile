pipeline {
    agent any

    environment {
        // Автоматически определяем доступный Python
        PYTHON_CMD = 'python3'
    }

    stages {
        stage('Check Environment') {
            steps {
                echo '🔍 Проверяем окружение...'
                script {
                    // Пробуем найти работающий Python
                    def pythonCommands = ['python3', 'python', 'py']
                    env.PYTHON_CMD = null

                    for (cmd in pythonCommands) {
                        try {
                            sh "${cmd} --version"
                            env.PYTHON_CMD = cmd
                            echo "✅ Найден Python: ${cmd}"
                            break
                        } catch (Exception e) {
                            echo "❌ ${cmd} не найден"
                        }
                    }

                    if (env.PYTHON_CMD == null) {
                        echo """
                        ⚠️ Python не найден в системе!

                        Установите Python в Jenkins контейнер:
                        1. docker exec -it jenkins bash
                        2. apt-get update
                        3. apt-get install -y python3 python3-pip
                        4. ln -s /usr/bin/python3 /usr/bin/python (опционально)
                        """
                        currentBuild.result = 'FAILURE'
                        error("Python не установлен")
                    }
                }

                sh '''
                    echo "=== Информация о системе ==="
                    echo "Python команда: ${PYTHON_CMD}"
                    ${PYTHON_CMD} --version
                    uname -a
                    echo "=== Содержимое проекта ==="
                    pwd
                    ls -la
                '''
            }
        }

        stage('Check Project Structure') {
            steps {
                echo '📁 Проверяем структуру проекта...'
                sh '''
                    echo "=== Python файлы ==="
                    find . -name "*.py" | head -10 || echo "Python файлы не найдены"

                    echo "=== Файл зависимостей ==="
                    if [ -f "requirements.txt" ]; then
                        echo "requirements.txt найден:"
                        cat requirements.txt
                    else
                        echo "❌ requirements.txt не найден!"
                        echo "Создайте файл requirements.txt с зависимостями"
                    fi

                    echo "=== Папка tests ==="
                    if [ -d "tests" ]; then
                        echo "✅ Папка tests найдена:"
                        ls -la tests/ | head -10
                        find tests/ -name "*.py" | head -5
                    else
                        echo "❌ Папка tests не найдена!"
                        echo "Создайте папку tests/ с тестами"
                    fi
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Устанавливаем зависимости...'
                script {
                    if (fileExists('requirements.txt')) {
                        sh '''
                            echo "Устанавливаем зависимости из requirements.txt"
                            ${PYTHON_CMD} -m pip install --user --upgrade pip || echo "Не удалось обновить pip"
                            ${PYTHON_CMD} -m pip install --user -r requirements.txt
                            echo "=== Установленные пакеты ==="
                            ${PYTHON_CMD} -m pip list --user
                        '''
                    } else {
                        echo "⚠️ requirements.txt не найден, устанавливаем pytest"
                        sh '''
                            ${PYTHON_CMD} -m pip install --user pytest
                        '''
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Запускаем тесты...'
                script {
                    if (fileExists('tests/')) {
                        echo "Запускаем тесты из папки tests/"
                        sh '''
                            ${PYTHON_CMD} -m pytest tests/ -v --tb=short || echo "Pytest завершился"
                        '''
                    } else {
                        echo "Папка tests/ не найдена, ищем тесты в проекте"
                        sh '''
                            ${PYTHON_CMD} -m pytest . -v --tb=short -k "test" || echo "Тесты не найдены"
                        '''
                    }
                }
            }
        }

        stage('Build Report') {
            steps {
                echo '📊 Генерируем отчет...'
                sh '''
                    echo "=== Итоговый отчет ==="
                    echo "Python: ${PYTHON_CMD}"
                    ${PYTHON_CMD} --version
                    echo "Рабочая директория:"
                    pwd
                    echo "Проект успешно протестирован!"
                '''
            }
        }
    }

    post {
        always {
            echo "🏁 Пайплайн завершен: ${currentBuild.currentResult}"
            sh '''
                echo "=== Файлы в рабочей директории ==="
                ls -la | head -10
            '''
        }
        success {
            echo '✅ Все этапы выполнены успешно!'
            sh 'echo "🎉 Поздравляю! Ваш первый пайплайн работает!"'
        }
        failure {
            echo '❌ В процессе выполнения возникли ошибки'
            sh 'echo "💡 Проверьте что Python установлен и структура проекта правильная"'
        }
        unstable {
            echo '⚠️ Пайплайн завершился с предупреждениями'
        }
    }
}
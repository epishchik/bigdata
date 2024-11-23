# Домашнее задание 1
## Инструкция по развертыванию кластера hadoop
* 1\. Работаем на jump node.
    - 1.1 Зайдем на jump-node `ssh team@external_jn_ip`.
    - 1.2 Добавим пользователя hadoop `sudo adduser hadoop`.
    - 1.3 Сменим активного пользователя на hadoop `sudo -i -u hadoop`.
    - 1.4 Сгенерируем для него ssh ключи `ssh-keygen`.
    - 1.5 Сохраним публичный ключ себе `cat /home/hadoop/.ssh/id_ed25519.pub`, понадобится в дальшем.
    - 1.6 Скачаем дистрибутив hadoop `wget https://archive.apache.org/dist/hadoop/common/hadoop-3.4.0/hadoop-3.4.0.tar.gz`.
    - 1.7 Выйдем из пользователя hadoop `exit`.
    - 1.8 Редактируем файл с хостами, чтобы отключить локальную аддресацию `sudo nano /etc/hosts`. Комментируем все адреса и вставляем адреса нод с названием.
    ```
    local_jn_ip team-30-jn
    local_nn_ip team-30-nn
    local_dn0_ip team-30-dn-0
    local_dn1_ip team-30-dn-1
    ```
    - 1.9 Проверим, что все ноды пингуются по имени `ping team-30-jn`, `ping team-30-nn`, `ping team-30-dn-0`, `ping team-30-dn-1`.
* 2\. Работаем на name node.
    - 2.1 Заходим на сервер, где будет неймнода `ssh team-30-nn`.
    - 2.2 Проделываем пункты (в указанном порядке) 1.8-1.9, 1.2 - 1.5 на этом сервере.
    - 2.3 Выходим с юзера `exit`.
    - 2.4 Выходим с неймноды `exit`.
* 3\. Работаем на первой data node.
    - 3.1 Заходим на сервер, где будет дата нода `ssh team-30-dn-0`.
    - 3.2 Проделываем пункты (в указанном порядке) 1.8-1.9, 1.2 - 1.5 на этом сервере.
    - 3.3 Выходим с юзера `exit`.
    - 3.4 Выходим с неймноды `exit`.
* 4\. Работаем на второй data node.
    - 4.1 Заходим на сервер, где будет дата нода `ssh team-30-dn-1`.
    - 4.2 Проделываем пункты (в указанном порядке) 1.8-1.9, 1.2 - 1.5 на этом сервере.
    - 4.3 Выходим с юзера `exit`.
    - 4.4 Выходим с неймноды `exit`.
* 5\. Работаем на jump node.
    - 5.1 Сменим активного пользователя на hadoop `sudo -i -u hadoop`.
    - 5.2 Создаем файл, где будем хранить ключи ssh для авторизации без пароля `nano .ssh/authorized_keys`.
    - 5.3 Положим 4 публичных ключа, которые сохранили до этого.
    - 5.4 Откопируем файл с ключами на все ноды (используется пароль от юзера hadoop, который мы задавали при создании юзера) `scp .ssh/authorized_keys team-30-nn:/home/hadoop/.ssh/`, `scp .ssh/authorized_keys team-30-dn-0:/home/hadoop/.ssh/`, `scp .ssh/authorized_keys team-30-dn-1:/home/hadoop/.ssh/`.
    - 5.5 Откопируем архив с дистрибутивом hadoop на все ноды `scp hadoop-3.4.0.tar.gz team-30-nn:/home/hadoop/`, `scp hadoop-3.4.0.tar.gz team-30-dn-0:/home/hadoop/`, `scp hadoop-3.4.0.tar.gz team-30-dn-1:/home/hadoop/`.
* 6\. На каждой из трех нод (nn, dn-0, dn-1)
    - 6.1 Далее все шаги выполняются под пользователем hadoop.
    - 6.2 Распакуем архив с hadoop `tar -xvzf hadoop-3.4.0.tar.gz`.
* 7\. Работаем на name node.
    - 7.1 Далее все шаги выполняются под пользователем hadoop.
    - 7.2 Находим путь к java `which java` и считываем симлинк по полученному пути `readlink -f /usr/bin/java`.
    - 7.3 Добавим необходимые переменные окружения в файл `nano ~/.profile`, вставим приведенные ниже строки.
    ```
    export HADOOP_HOME=/home/hadoop/hadoop-3.4.0
    export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
    export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
    ```
    - 7.4 Перезагрузим окружение `source ~/.profile`.
    - 7.5 Проверим, что все подтянулось `hadoop version`.
    - 7.6 Копируем ~/.profile на дата ноды `scp ~/.profile team-30-dn-0:/home/hadoop/`, `scp ~/.profile team-30-dn-1:/home/hadoop/`.
    - 7.7 Переходим в папку дистрибутива hadoop `cd ~/hadoop-3.4.0/etc/hadoop/`.
    - 7.8 Добавляем переменную JAVA_HOME в файл hadoop-env.sh, делаем `nano hadoop-env.sh` и добавляем строчку `JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64`.
    - 7.9 Копируем файл hadoop-env.sh на дата ноды `scp hadoop-env.sh team-30-dn-0:/home/hadoop/hadoop-3.4.0/etc/hadoop/`, `scp hadoop-env.sh team-30-dn-1:/home/hadoop/hadoop-3.4.0/etc/hadoop/`.
    - 7.10 Редактируем файл core-site.xml, наша конфигурация лежит в репозитории в файле [core-site.xml](configs/core-site.xml).
    - 7.11 Редактируем файл hdfs-site.xml, наша конфигурация лежит в репозитории в файле [hdfs-site.xml](configs/hdfs-site.xml).
    - 7.12 Из файла workers удаляем запись localhost и добавляем строки с названием наших нод.
    ```
    team-30-nn
    team-30-dn-0
    team-30-dn-1
    ```
    - 7.13 Копируем файлы core-site.xml, hdfs-site.xml и workers на дата ноды `scp core-site.xml hdfs-site.xml workers team-30-dn-0:/home/hadoop/hadoop-3.4.0/etc/hadoop/`, `scp core-site.xml hdfs-site.xml workers team-30-dn-1:/home/hadoop/hadoop-3.4.0/etc/hadoop/`.
    - 7.14 Переходим в ~/hadoop-3.4.0 `cd ~/hadoop-3.4.0` и форматируем файловую систему `bin/hdfs namenode -format`.
    - 7.15 Запускаем отформатированную файловую систему `sbin/start-dfs.sh`.
    - 7.16 Убедимся, что запущены демоны NameNode, DataNode и SecondaryNameNode `jps` на team-30-nn и по одному демону DataNode на team-30-dn-0 и team-30-dn-1.

## Поднимаем веб-интерфейс для hadoop
* 1\. Работаем на jump node, поднимаем веб-интерфейс для name node.
    - 1.1 Копируем конфиг nginx для нашей team-30-nn `sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/nn`.
    - 1.2 Редактируем конфиг так, чтобы доступ к веб-интерфейсу можно было получить с jump node, наша конфигурация лежит в репозитории в файле [nn](configs/nginx/nn).
    - 1.3 Создаем симлинк `sudo ln -s /etc/nginx/sites-available/nn /etc/nginx/sites-enabled/nn`.
    - 1.4 Перезапускаем nginx `sudo systemctl reload nginx`.
    - 1.5 Веб-интерфейс доступен по пути `http://external_jn_ip:9870/`.

# Домашнее задание 2
## Инструкция по развертыванию YARN
* 1\. Редактируем конфиги `mapred-site.xml` и `yarn-site.xml`
    - 1.1 С помощью `ssh team@external_jn_ip` заходим на jump node
    - 1.2 Меняем юзера на `hadoop` с помощью `sudo -i -u hadoop`
    - 1.3 Переходим на name node, используя `ssh team-30-nn`
    - 1.4 Меняем конфигурацию файла `/home/hadoop/hadoop-3.4.0/etc/hadoop/mapred-site.xml` на [mapred-site.xml](configs/mapred-site.xml)
    - 1.5 Меняем конфигурацию файла `/home/hadoop/hadoop-3.4.0/etc/hadoop/yarn-site.xml` на [yarn-site.xml](configs/yarn-site.xml)
    - 1.6 Копируем получившиеся конфиги на data nodes с помощью
    ```
    scp mapred-site.xml yarn-site.xml team-30-dn-0:/home/hadoop/hadoop-3.4.0/etc/hadoop
    scp mapred-site.xml yarn-site.xml team-30-dn-1:/home/hadoop/hadoop-3.4.0/etc/hadoop
    ```
    - 1.7 Запускаем YARN из `/home/hadoop/hadoop-3.4.0/` командой `./sbin/start-yarn.sh`
    - 1.8 Запускаем historyserver с помощью `mapred --daemon start historyserver`

## Поднимаем веб-интерфейс для YARN и historyserver
* 1\. Будем редактировать конфигурации reverse-proxy сервера nginx для YARN и history server
    - 1.1 С помощью `ssh team@external_jn_ip` заходим на jump node
    - 1.2 Создаем файлы [ya](configs/nginx/ya) и [dh](configs/nginx/dh) в директории `/etc/nginx/sites-available/`
    - 1.3 Создаем сим линки
    ```
    sudo ln -s /etc/nginx/sites-available/dh /etc/nginx/sites-enabled/dh
    sudo ln -s /etc/nginx/sites-available/ya /etc/nginx/sites-enabled/ya
    ```
    - 1.4 Перезапускаем nginx `sudo systemctl reload nginx`
    - 1.5 Веб интерфейс YARN доступен по адресу `http://external_jn_ip:8088/`, веб интерфейс historyserver доступен по адресу `http://external_jn_ip:19888/`
 
  # Домашнее задание 3
* 1\. Работаем на name node.
    - 1.1 Зайдем на jump-node `ssh team@external_jn_ip`.
    - 1.2 Сменим активного пользователя на hadoop `sudo -i -u hadoop`.
    - 1.3 Зайдем на name-node `ssh team-30-nn`.
    - 1.4 Скачаем дистрибутив hive `wget https://archive.apache.org/dist/hive/hive-4.0.0-alpha-2/apache-hive-4.0.0-alpha-2-bin.tar.gz`.
    - 1.5 Распакуем его `tar -xzvf apache-hive-4.0.0-alpha-2-bin.tar.gz`
    - 1.6 Перейдём в папку с hive `cd apache-hive-4.0.0-alpha-2-bin/`
    - 1.7 Пропишем пути в ~/.profile
      ```
      export HIVE_HOME=/home/hadoop/apache-hive-4.0.0-alpha-2-bin
      export PATH=$HIVE_HOME/bin:$PATH
      ```
    - 1.8 Выполним `source ~/.profile`
    - 1.9 Выполним следующие команды```
      hdfs dfs -mkdir /tmp # выполнить если такой папки нет
      hdfs dfs -mkdir -p /user/hive/warehouse
      hdfs dfs -chmod g+w /tmp
      hdfs dfs -chmod g+w /user/hive/warehouse```
      Если появляется ошибка с "safe mode" выполнить `hdfs namenode -format` и повторить заново
    - 1.10 Инициализируем базу данных hive командой `bin/schematool -dbType derby -initSchema`
    - 1.11 Запустим hive `hive --hiveconf hive.server2.enable.doAs=false      --hiveconf hive.security.authorization.enabled=false      --service hiveserver2 1>> /tmp/hs2.log 2>> /tmp/hs2.log &`
    - 1.12 Запустим утилиту hive `beeline -u jdbc:hive2://localhost:10000 -n scott -p tiger`
    - 1.13 Создадим базу данных `CREATE DATABASE test;`
    - 1.14 Создадим таблицу
      ```
      CREATE TABLE IF NOT EXISTS test.poetry (
            rating int,
            views int,
            genre string
      )
      COMMENT 'poetry table'
      ROW FORMAT DELIMITED 
      FIELDS TERMINATED BY '\t';
      ```
    - 1.15 Загрузим данные в таблицу (предварительно загрузив на hdfs) `load data inpath '/tmp/data.tsv' into table test.poetry`
    - 1.16 Создадим партицированную таблицу
      ```
      CREATE TABLE IF NOT EXISTS test.poetry_final (
            rating int,
            views int
      )
      COMMENT 'poetry table final'
      PARTITIONED BY (genre string)
      ROW FORMAT DELIMITED 
      FIELDS TERMINATED BY '\t';
      ```
    - 1.17 Загрузим в неё данные из предыдущей таблицы
      ```
      INSERT INTO TABLE test.poetry_final PARTITION (genre)
      SELECT rating, views, genre
      FROM test.poetry
      WHERE rating IS NOT NULL;
      ```
      
    

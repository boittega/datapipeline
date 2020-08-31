SCHEDULER_PID=$(<~/airflow/airflow-scheduler.pid)
WEBSERVER_MONITOR_PID=$(<~/airflow/airflow-webserver-monitor.pid)

echo Gracefully shutting down Airflow
kill -TERM $SCHEDULER_PID
while kill -0 $WEBSERVER_MONITOR_PID 2> /dev/null; do
    echo waiting for webserver to shutdown
    kill -TERM $WEBSERVER_MONITOR_PID
    sleep 1
done
echo Airflow shut down

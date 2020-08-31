
BASEPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

export AIRFLOW__CORE__LOAD_EXAMPLES=false
export AIRFLOW__CORE__DAGS_FOLDER=${BASEPATH%%/}/dags
export AIRFLOW__CORE__PLUGINS_FOLDER=${BASEPATH%%/}/plugins

airflow webserver -D
airflow scheduler -D

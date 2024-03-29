#Check if the first parameter is present
if [ $# -eq 0 ]
  then
    echo "Bad parameter : ./start.sh your_ip_adress"
    echo "Example : ./start.sh 192.168.1.30"
    echo "You can found your ip adress with the command 'ifconfig'"
    exit -1
fi

#Check if Flask_app is present
if [ $(printenv | grep -c 'FLASK_APP') -eq 0 ]
then
	echo "Export Flask App"
	export FLASK_APP=coinbase_api.py
fi

#Check if Flask_debug is present
if [ $(printenv | grep -c 'FLASK_DEBUG') -eq 0 ]
then
	echo "Export Flask Debug"
	export FLASK_DEBUG=true
fi

if [ $(printenv | grep -c 'API_SECRET') -eq 0 ]
then
  echo "Don't forget of export your API_SECRET"
  echo "Example : export API_SECRET=aaaaaaaaaa"
  exit -1
fi

if [ $(printenv | grep -c 'API_KEY') -eq 0 ]
then
  echo "Don't forget of export your API_KEY"
  echo "Example : export API_KEY=aaaaaaaaaa"
  exit -1
fi

#Run Flask on adress with python2
python -m flask run -h "$1"

#Change project id and namespace here
projectid=<gcp-project-id>
namespace=<ns>
gkecluster=<gke-cluster-name>
#replacing wth project id
sed -i 's/projectid/{$projectid}/g' deployment.yaml
echo "Cloning Spring boat application"
#git clone https://github.com/spring-projects/spring-petclinic
sleep 5
echo "Builiding application with docker"
docker build --tag  gcr.io/$projectid/pgsql-client .
sleep 5
docker push gcr.io/$projectid/pgsql-client
# switching to training cluster
gcloud container clusters  get-credentials $gkecluster
sleep 5
kubectl apply -f deployment.yaml -n $namespace
sleep 5
kubectl apply -f service.yaml -n $namespace
sleep 5


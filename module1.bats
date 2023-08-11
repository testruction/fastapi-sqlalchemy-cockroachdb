#!/usr/bin/env bats


# @test "M1S1: Clone the Web application source code" {
#   git clone https://github.com/testruction/fastapi-sqlalchemy-cockroachdb
# 
#   git checkout -b feature/helm-chart
# }

@test "M1S2: Created initial chart" {


  helm create ./chart

  echo '**/charts/*.tgz' | tee -a .gitignore
}

@test "M1S3: Create and populate components directories" {


  mkdir -p chart/templates/backend chart/templates/frontend
  cp chart/templates/*.yaml chart/templates/backend/
  cp chart/templates/*.yaml chart/templates/frontend/
  rm -vf chart/templates/*.yaml
}

@test "M1S4: Create configuration sections for earch components" {


  cat chart/values.yaml | head -4 > /tmp/values.yaml

  tail +5 chart/values.yaml | yq '{"backend": .}' >> /tmp/values.yaml
  tail +5 chart/values.yaml | yq '{"frontend": .}' >> /tmp/values.yaml

  yq /tmp/values.yaml
  mv /tmp/values.yaml chart/values.yaml
}

@test "M1S5: Add conditions to control the deployment" {


  yq -i '.backend.enabled = true' chart/values.yaml
  yq -i '.frontend.enabled = true' chart/values.yaml
}

@test "M1S6: Record changes to the Git history" {


  git config user.name 'Helm Student'
  git config user.email 'student.helm@testruction.lab'

  git add .
  git status
  git status -v

  git commit -m 'Initial helm chart commit'
}

@test "M1S6: Reflect the new configuration structure in the templates" {


  # Backend
  sed -i 's/\.Values\./.Values.backend./g' chart/templates/backend/*.yaml

  # Frontend
  sed -i 's/\.Values\./.Values.frontend./g' chart/templates/frontend/*.yaml

  git add .
  git status -v
  git commit -m 'Updated configuration values'
}

@test "M1S8: Suffix Kubernetes resources" {


  # Backend
  sed -i 's/^\(\s\{2\}name\:\s.*\)$/\1-backend/g' chart/templates/backend/*.yaml

  # Frontend
  sed -i 's/^\(\s\{2\}name\:\s.*\)$/\1-frontend/g' chart/templates/frontend/*.yaml

  # Service Account references
  sed -i 's/^\(\s\{6\}serviceAccountName\:\s.*\)$/\1-backend/g' chart/templates/backend/*.yaml
  sed -i 's/^\(\s\{6\}serviceAccountName\:\s.*\)$/\1-frontend/g' chart/templates/frontend/*.yaml

  # Ingress references
  sed \
  -e 's#^\(\s\{16\}name\:\s.*\)#\1-backend#g' \
  -e 's#^\(\s\{14\}serviceName\:\s.*\)#\1-backend#g' \
  -i chart/templates/backend/ingress.yaml

  sed \
  -e 's#^\(\s\{16\}name\:\s.*\)#\1-frontend#g' \
  -e 's#^\(\s\{14\}serviceName\:\s.*\)#\1-frontend#g' \
  -i chart/templates/frontend/ingress.yaml

  git add .
  git status -v
  git commit -m 'Added component suffix to resources name'
}

@test "M1S9: Allocate distinct container images" {


  yq -i '.backend.image.repository = "ghcr.io/testruction/fastapi-sqlalchemy-cockroachdb/backend"' chart/values.yaml
  yq -i '.frontend.image.repository = "ghcr.io/testruction/fastapi-sqlalchemy-cockroachdb/frontend"' chart/values.yaml
}

@test "M1S10: Update containers ports" {


  sed -i 's/containerPort: 80/containerPort: 8000/g' chart/templates/backend/deployment.yaml
  sed -i 's/containerPort: 80/containerPort: 8000/g' chart/templates/frontend/deployment.yaml

  sed -i 's#path: /#path: /health#g' chart/templates/*/deployment.yaml

  git commit -a -m 'Allocated application service ports'
}

@test "M1S11: Update Chart packaging specifications" {


  export SOURCE_URL=$(git config --get remote.origin.url)

  yq -i '.sources[0] = strenv(SOURCE_URL)' chart/Chart.yaml
  yq -i '.home = strenv(SOURCE_URL)' chart/Chart.yaml
  yq -i '.name = "fastapi"' chart/Chart.yaml
  yq -i '.description = strenv(SOURCE_URL)' chart/Chart.yaml
  yq -i '.appVersion = "1.1.1"'  chart/Chart.yaml

  git commit -a -m 'Added source URL to chart definition'
}

@test "M1S12: Create tests" {


  cp -v chart/templates/tests/test-connection.yaml \
        chart/templates/tests/test-backend-service.yaml

  sed \
  -e 's#\(test\)-connection#\1-backend-service#g' \
  -e 's#\(\}\}\)\(:\)#\1-backend\2#g' \
  -e 's#\(.Values\)\(.service.port\)#\1.backend\2#g' \
  -e 's#\(.service.port\s\}\}\)#\1/apis/v1/fakenames?limit=5#g' \
  -i chart/templates/tests/test-backend-service.yaml

  cp -v chart/templates/tests/test-connection.yaml \
      chart/templates/tests/test-frontend-service.yaml

  sed \
  -e 's#\(test\)-connection#\1-frontend-service#g' \
  -e 's#\(\}\}\)\(:\)#\1-frontend\2#g' \
  -e 's#\(.Values\)\(.service.port\)#\1.frontend\2#g' \
  -i chart/templates/tests/test-frontend-service.yaml

  rm -f chart/templates/tests/test-connection.yaml
}

@test "M1S13: Update helpers script and deployment notes" {


  yq -i '
  .global.serviceAccount.create = true |
  .global.serviceAccount.name = ""
  ' chart/values.yaml

  sed -i 's#\(.Values\)\(.serviceAccount\)#\1.global\2#g' chart/templates/_helpers.tpl

  sed \
  -e 's#\(.Values\)\(.*\)#\1.frontend\2#g' \
  -i chart/templates/NOTES.txt
}

@test "Finalize: Commit changes" {


  helm template --dry-run chart/

  git commit -a -m 'Finalized initial chart developement'
}

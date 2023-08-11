#!/usr/bin/env bats

@test "M2S2: Add environment variables support" {


  yq -i '
    .backend.env = [] |
    .backend.extraEnv = [] |
    .frontend.env = [] |
    .frontend.extraEnv = []
  ' chart/values.yaml
}

@test "M2S3: Add trace collector dependency" {


  yq -i '
    .dependencies[0].name = "jaeger" |
    .dependencies[0].condition = "jaeger.enabled" |
    .dependencies[0].repository = "https://jaegertracing.github.io/helm-charts" |
    .dependencies[0].version = "0.71.10"
  ' chart/Chart.yaml

  helm dependency update chart/
}

@test "M2S4: Add the Jaeger deployment configuration" {


  yq -i '
    .jaeger.enabled = true |
    .jaeger.allInOne.enabled = true |
    .jaeger.ingester.enabled = false |
    .jaeger.agent.enabled = false |
    .jaeger.collector.enabled = false |
    .jaeger.query.enabled = false |
    .jaeger.spark.enabled = false |
    .jaeger.hotrod.enabled = false |
    .jaeger.provisionDataStore.cassandra = false
  ' chart/values.yaml

  helm template chart/ | grep 'kind' | wc -l
}

@test "M2S5: Configure backend and frontend environment variables" {


  yq -i '
    .jaeger.extraEnv[0].name = "COLLECTOR_OTLP_ENABLED" |
    .jaeger.extraEnv[0].value = true |
    .backend.env[0].name = "OTEL_RESOURCE_ATTRIBUTES" |
    .backend.env[0].value = "service.namespace=io.testruction,service.name=backendservice" |
    .frontend.env[0].name = "OTEL_RESOURCE_ATTRIBUTES" |
    .frontend.env[0].value = "service.namespace=io.testruction,service.name=frontendservice"
  ' chart/values.yaml

  yq -i '
    .backend.tracing.url = null |
    .backend.tracing.insecure = true |
    .frontend.tracing.url = null |
    .frontend.tracing.insecure = true
  ' chart/values.yaml
}

@test "M2S6: Implement backend environment variables" {


  run vi -e chart/templates/backend/deployment.yaml <<EOF
/ports
i
          env:
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: http{{ if not .Values.backend.tracing.insecure }}s{{ end }}://{{ default "localhost" (print .Release.Name "-jaeger-collector") }}:4317
            - name: OTEL_EXPORTER_OTLP_INSECURE
              value: {{ .Values.backend.tracing.insecure | quote }}
            {{- with (concat .Values.frontend.env .Values.frontend.extraEnv )}}
              {{- toYaml . | nindent 12 }}
            {{- end }}
.
wq
EOF
}

@test "M2S7: Implement frontend environment variables" {


  run vi -e chart/templates/frontend/deployment.yaml <<EOF
/ports
i
          env:

            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: http{{ if not .Values.frontend.tracing.insecure }}s{{ end }}://{{ default "localhost" (print .Release.Name "-jaeger-collector") }}:4317
            - name: OTEL_EXPORTER_OTLP_INSECURE
              value: {{ .Values.frontend.tracing.insecure | quote }}
            - name: BACKEND_API_URL
              {{- \$fullName := include "chart.fullname" . }}
              value: {{ print "http://" \$fullName "-backend:" .Values.backend.service.port | quote }}
            {{- with (concat .Values.frontend.env .Values.frontend.extraEnv )}}
              {{- toYaml . | nindent 12 }}
            {{- end }}
.
wq
EOF
}

@test "Finalize: Commit changes" {


  helm template chart/

  git commit -a -m "Add trace collector support"
}

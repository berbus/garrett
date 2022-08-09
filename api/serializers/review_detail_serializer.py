from rest_framework import serializers

import api.models as models
import api.services as services


class ReviewDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        fields = '__all__'

    security_tests = serializers.SerializerMethodField(read_only=True)
    threat_models = serializers.SerializerMethodField(read_only=True)
    jira_issue = serializers.SerializerMethodField(read_only=True)
    services = serializers.SerializerMethodField()

    def get_services(self, review):
        services = []
        _ = [
            services.append({
                'oid': str(service.oid),
                'name': service.name
            }) for service in review.services.all()
        ]
        return services

    def get_security_tests(self, review):
        security_tests = models.SecurityTest.objects.filter(review=review)
        res = []

        for security_test in security_tests:
            t = {}
            t['oid'] = security_test.oid
            t['title'] = security_test.title
            t['creation_date'] = security_test.creation_date
            t['completion_date'] = security_test.completion_date
            t['template'] = {
                'oid': str(security_test.template.oid),
                'name': security_test.template.name,
            }
            t['service'] = security_test.service.name
            res.append(t)
        return res

    def get_threat_models(self, review):
        threat_models = models.ThreatModel.objects.filter(review=review)
        res = []

        for threat_model in threat_models:
            t = {}
            t['oid'] = threat_model.oid
            t['title'] = threat_model.title
            t['creation_date'] = threat_model.creation_date
            t['completion_date'] = threat_model.completion_date
            t['service'] = threat_model.service.name
            res.append(t)
        return res

    def get_jira_issue(self, review):
        res = None
        if review.jira_issue:
            res = {
                'oid': review.jira_issue.oid,
                'jira_id': review.jira_issue.jira_id,
                'url': services.jira.get_url_for_issue(review.jira_issue)
            }
        return res

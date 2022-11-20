from rest_framework import serializers

import api.models as models


class ServiceDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service
        fields = '__all__'

    reviews = serializers.SerializerMethodField()

    def get_reviews(self, service):
        res = []
        reviews = models.Review.objects.filter(services=service).order_by('-creation_date')
        for review in reviews:
            review_data = {
                'oid': review.oid,
                'title': review.title,
                'creation_date': review.creation_date,
                'completion_date': review.completion_date
            }
            if review.jira_issue:
                review_data['jira_issue'] = {
                    'jira_key': review.jira_issue.jira_key,
                    'jira_id': review.jira_issue.jira_id
                }
            res.append(review_data)

        return res

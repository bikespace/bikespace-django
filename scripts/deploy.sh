#!/bin/bash
case "$ENV" in
  staging)
    BUCKET="bikespace-staging-static"
    ;;
  prod)
    BUCKET="bikespace-static"
    ;;
  *)
    exit 1
    ;;
esac

(
  cd bicycleparking
  npm install
  npm install --dev
  npm run $ENV
)
python3 manage.py collectstatic --noinput
dpl --provider=s3 \
  --local-dir="Bicycle_parking/staticfiles" \
  --acl=public_read \
  --access-key-id="$AWS_ACCESS_KEY_ID" \
  --secret-access-key="$AWS_SECRET_ACCESS_KEY" \
  --bucket="$BUCKET" \
  --region="us-east-1" \
  --default_text_charset="utf-8" \
  --skip-cleanup

if [ "$ENV" == "prod" ]; then
  dpl --provider=elasticbeanstalk \
    --access-key-id="$AWS_ACCESS_KEY_ID" \
    --secret-access-key="$AWS_SECRET_ACCESS_KEY" \
    --app="bikespace" \
    --env="bikespace-django22-prod-env" \
    --region="us-east-1" \
    --bucket_name="$ELB_BUCKET_NAME"
fi

if [ "$ENV" == "staging" ]; then
  dpl --provider=heroku \
    --app="torontobikeparking-staging" \
    --api-key="$HEROKU_STAGING_API_KEY"
fi

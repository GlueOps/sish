# GlueOps Sish Docker Compose

## Quick Start

1. Copy the environment template and configure your values:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your settings:
   ```
   DOMAIN=ssh.example.com
   ACME_EMAIL=admin@example.com
   AWS_ACCESS_KEY_ID=your_access_key_id
   AWS_SECRET_ACCESS_KEY=your_secret_access_key
   ```

3. Start the stack:
   ```bash
   docker-compose up -d
   ```

## SSL Certificates

Certificates are automatically generated via Let's Encrypt using DNS01 challenge with AWS Route53. The stack obtains both `${DOMAIN}` and `*.${DOMAIN}` (wildcard) certificates.

### How it works

- **dnsrobocert** handles certificate issuance and renewal via Route53
- On renewal, `deploy-hook.sh` copies certs to the shared `ssl` volume
- **sish** watches the certificate directory and reloads automatically (200ms polling)

### AWS IAM Permissions

The IAM user needs the following Route53 permissions:
- `route53:ListHostedZones`
- `route53:GetChange`
- `route53:ChangeResourceRecordSets`
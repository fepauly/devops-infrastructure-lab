# Ansible Configuration

## Collection Compatibility

This project uses Ansible 2.12.x with specifically chosen collection versions for compatibility:

- **community.general**: 5.8.0 - Last version with full Ansible 2.12 support
- **community.postgresql**: 2.4.0 - Stable PostgreSQL management
- **community.docker**: 2.7.6 - Docker container management

## Managing Collections

### Installing Collections
```bash
# Install from requirements file (recommended)
ansible-galaxy collection install -r requirements.yml

# Or install specific versions manually
ansible-galaxy collection install community.general:==5.8.0
```

### Updating Collections
When updating, ensure compatibility with your Ansible version:
```bash
# Check current versions
ansible-galaxy collection list

# Update to specific compatible versions
ansible-galaxy collection install -r requirements.yml --force
```

### Troubleshooting
If you see warnings about unsupported versions:
1. Check the collection's GitHub page for compatibility matrix
2. Use an older collection version that supports your Ansible version
3. Consider upgrading Ansible if newer features are needed

## Best Practices
- Always pin collection versions in production
- Test collection updates in development first
- Document version compatibility for your team

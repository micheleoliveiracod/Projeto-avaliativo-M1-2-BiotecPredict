#!/bin/bash

# Script para configurar Branch Protection Rules no GitHub
# Requer: GitHub CLI (gh) instalado e autenticado
# Uso: ./setup_branch_protection.sh

set -e

REPO="micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict"
MAIN_BRANCH="main"
DEVELOP_BRANCH="develop"

echo "🔒 Configurando Branch Protection Rules..."
echo ""

# Verificar se GitHub CLI está instalado
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI não está instalado!"
    echo "📥 Instale em: https://cli.github.com/"
    exit 1
fi

# Verificar autenticação
if ! gh auth status &> /dev/null; then
    echo "❌ Não autenticado no GitHub!"
    echo "🔑 Execute: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI autenticado"
echo ""

# ============================================
# Configurar proteção para branch 'main'
# ============================================
echo "🔐 Configurando proteção para branch 'main'..."

gh api repos/$REPO/branches/$MAIN_BRANCH/protection \
  --input - << 'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "backend-lint",
      "backend-tests",
      "frontend-lint",
      "frontend-tests",
      "api-integration-tests",
      "build-status"
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_conversation_resolution": true,
  "required_linear_history": false
}
EOF

echo "✅ Branch 'main' protegida!"
echo ""

# ============================================
# Configurar proteção para branch 'develop'
# ============================================
echo "🔐 Configurando proteção para branch 'develop'..."

gh api repos/$REPO/branches/$DEVELOP_BRANCH/protection \
  --input - << 'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "backend-lint",
      "backend-tests",
      "frontend-lint",
      "frontend-tests",
      "api-integration-tests",
      "build-status"
    ]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_conversation_resolution": true,
  "required_linear_history": false
}
EOF

echo "✅ Branch 'develop' protegida!"
echo ""

echo "✅ ✅ ✅ Branch Protection Rules configuradas com sucesso!"
echo ""
echo "📋 Resumo:"
echo "  • main: Exigir 1 aprovação + testes passando"
echo "  • develop: Exigir 1 aprovação + testes passando"
echo "  • Ambas: Sem force push, sem deletions"

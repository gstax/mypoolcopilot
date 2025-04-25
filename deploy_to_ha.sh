#!/bin/bash

# === Configuration ===
REPO_NAME="mypoolcopilot"
INTEGRATION_NAME="poolcopilot"
HA_CUSTOM_COMPONENTS_PATH="/config/custom_components"

echo "🔄 Déploiement local de l'intégration Home Assistant : $INTEGRATION_NAME"
echo "📁 Dossier de destination : $HA_CUSTOM_COMPONENTS_PATH/$INTEGRATION_NAME"

# Vérification que le dossier source existe
if [ ! -d "custom_components/$INTEGRATION_NAME" ]; then
  echo "❌ Erreur : custom_components/$INTEGRATION_NAME n'existe pas."
  exit 1
fi

# Supprimer l'ancien dossier s’il existe déjà
if [ -d "$HA_CUSTOM_COMPONENTS_PATH/$INTEGRATION_NAME" ]; then
  echo "🗑 Suppression de l'ancienne version de l'intégration..."
  rm -rf "$HA_CUSTOM_COMPONENTS_PATH/$INTEGRATION_NAME"
fi

# Copier la nouvelle version
echo "📥 Copie des fichiers..."
cp -r "custom_components/$INTEGRATION_NAME" "$HA_CUSTOM_COMPONENTS_PATH/"

echo "✅ Intégration déployée avec succès !"
echo "🚀 Redémarre Home Assistant pour appliquer les changements."


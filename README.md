# NoteMaster v2

Application de prise de notes et de quiz pour les étudiants, avec authentification Google et stockage cloud.

## Configuration

1. Créer un projet sur [Supabase](https://supabase.com)
2. Activer l'authentification Google :
   - Dans votre projet Supabase : Authentication > Providers > Google
   - Configurer OAuth dans la [Console Google Cloud](https://console.cloud.google.com)
   - Ajouter les URLs de redirection autorisées

3. Copier le fichier `.env.example` en `.env` :
```bash
cp .env.example .env
```

4. Remplir les variables d'environnement dans `.env` :
```env
SUPABASE_URL=votre_url_supabase
SUPABASE_KEY=votre_clé_anon_supabase
OPENAI_API_KEY=votre_clé_api_openai
```

## Installation

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # ou "venv\Scripts\activate" sur Windows

# Installer les dépendances
pip install -r requirements.txt
```

## Lancement

```bash
streamlit run src/app.py
```

## Structure de la base de données Supabase

```sql
-- Table des notes
create table notes (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references auth.users not null,
  subject text not null,
  chapter text not null,
  title text not null,
  content text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Table des résultats de quiz
create table quiz_results (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references auth.users not null,
  question_id text not null,
  score numeric not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Politiques de sécurité
create policy "Users can only access their own notes"
  on notes for all
  using (auth.uid() = user_id);

create policy "Users can only access their own quiz results"
  on quiz_results for all
  using (auth.uid() = user_id);
```

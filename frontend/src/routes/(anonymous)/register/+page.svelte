<script lang="ts">
    import { goto } from "$app/navigation";

  // Variables pour le formulaire d'inscription
  let regPseudo = $state('');
  let regNom = $state('');
  let regPrenom = $state('');
  let regEmail = $state('');
  let regPassword = $state('');
  let regPasswordConfirm = $state('');
  
  // Fonction d'inscription
  function registration(formData) {
    console.log('Données d\'inscription:', formData);
    // Ici vous pouvez traiter les données d'inscription
    // Par exemple: validation, appel API, etc.
  }

  
  // Gestionnaire de soumission du formulaire d'inscription
  function handleRegistrationSubmit(event) {
    event.preventDefault();
    const formData = {
      pseudo: regPseudo,
      nom: regNom,
      prenom: regPrenom,
      email: regEmail,
      password: regPassword,
      passwordConfirm: regPasswordConfirm
    };
    registration(formData);
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-200 to-green-800 p-4">
  <div class="bg-white/95 backdrop-blur-lg rounded-3xl p-6 w-full max-w-md shadow-2xl border border-green-200">
    <!-- En-tête du formulaire -->
    <div class="text-center mb-10">
      <h1 class="text-4xl font-bold text-green-800 mb-2 drop-shadow">
        Inscription
      </h1>
      <p class="text-green-700 text-lg opacity-80">
        Créez votre nouveau compte
      </p>
    </div>
      <!-- Formulaire d'inscription -->
      <form onsubmit={handleRegistrationSubmit} class="space-y-6">
        <div class="space-y-2">
          <label for="reg-pseudo" class="block text-green-800 font-semibold text-sm tracking-wide">
            Pseudo
          </label>
          <input
            id="reg-pseudo"
            type="text"
            bind:value={regPseudo}
            placeholder="Votre pseudo"
            class="w-full px-5 py-4 border-2 border-green-200 rounded-xl text-green-800 placeholder-gray-400 transition-all duration-300 focus:border-green-500 focus:ring-4 focus:ring-green-100 focus:outline-none focus:-translate-y-0.5 bg-white/80 focus:bg-white"
            required
          />
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-2">
            <label for="reg-nom" class="block text-green-800 font-semibold text-sm tracking-wide">
              Nom
            </label>
            <input
              id="reg-nom"
              type="text"
              bind:value={regNom}
              placeholder="Nom"
              class="w-full px-5 py-4 border-2 border-green-200 rounded-xl text-green-800 placeholder-gray-400 transition-all duration-300 focus:border-green-500 focus:ring-4 focus:ring-green-100 focus:outline-none focus:-translate-y-0.5 bg-white/80 focus:bg-white"
              required
            />
          </div>
          
          <div class="space-y-2">
            <label for="reg-prenom" class="block text-green-800 font-semibold text-sm tracking-wide">
              Prénom
            </label>
            <input
              id="reg-prenom"
              type="text"
              bind:value={regPrenom}
              placeholder="Prénom"
              class="w-full px-5 py-4 border-2 border-green-200 rounded-xl text-green-800 placeholder-gray-400 transition-all duration-300 focus:border-green-500 focus:ring-4 focus:ring-green-100 focus:outline-none focus:-translate-y-0.5 bg-white/80 focus:bg-white"
              required
            />
          </div>
        </div>
        
        <div class="space-y-2">
          <label for="reg-email" class="block text-green-800 font-semibold text-sm tracking-wide">
            Adresse email
          </label>
          <input
            id="reg-email"
            type="email"
            bind:value={regEmail}
            placeholder="votre@email.com"
            class="w-full px-5 py-4 border-2 border-green-200 rounded-xl text-green-800 placeholder-gray-400 transition-all duration-300 focus:border-green-500 focus:ring-4 focus:ring-green-100 focus:outline-none focus:-translate-y-0.5 bg-white/80 focus:bg-white"
            required
          />
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-2">
            <label for="reg-password" class="block text-green-800 font-semibold text-sm tracking-wide">
              Mot de passe
            </label>
            <input
              id="reg-password"
              type="password"
              bind:value={regPassword}
              placeholder="••••••••"
              class="w-full px-5 py-4 border-2 border-green-200 rounded-xl text-green-800 placeholder-gray-400 transition-all duration-300 focus:border-green-500 focus:ring-4 focus:ring-green-100 focus:outline-none focus:-translate-y-0.5 bg-white/80 focus:bg-white"
              required
            />
          </div>
          
          <div class="space-y-2">
            <label for="reg-password-confirm" class="block text-green-800 font-semibold text-sm tracking-wide">
              Confirmer
            </label>
            <input
              id="reg-password-confirm"
              type="password"
              bind:value={regPasswordConfirm}
              placeholder="••••••••"
              class="w-full px-5 py-4 border-2 border-green-200 rounded-xl text-green-800 placeholder-gray-400 transition-all duration-300 focus:border-green-500 focus:ring-4 focus:ring-green-100 focus:outline-none focus:-translate-y-0.5 bg-white/80 focus:bg-white"
              required
            />
          </div>
        </div>
        
        <button 
          type="submit" 
          class="w-full bg-gradient-to-r from-green-500 to-green-800 text-white py-5 px-8 rounded-xl font-semibold text-lg uppercase tracking-wider transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-green-500/40 active:translate-y-0 mt-8"
        >
          S'inscrire
        </button>
        
        <div class="text-center pt-6">
          <p class="text-green-700">
            Déjà un compte ?
            <button 
              type="button" 
              onclick={() => goto("/login")} 
              class="text-green-500 font-semibold underline hover:text-green-800 transition-colors ml-1"
            >
              Se connecter
            </button>
          </p>
        </div>
      </form>
  </div>
</div>
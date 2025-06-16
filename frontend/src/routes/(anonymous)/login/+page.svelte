<script lang="ts">
    import { goto } from '$app/navigation';
    import type { LoginParams } from '$lib/authProvider';
    import authProvider from '$lib/authProvider';
    import { HttpError } from '$lib/error/httpError';
  
  // Variables pour le formulaire de connexion
  let loginUsername = $state('');
  let loginPassword = $state('');
  let loginError = $state('');
  
  async function login(formData: LoginParams) {
    try {
      await authProvider.login(formData)
      goto("/home")
    } catch (e) {
      if (e instanceof HttpError) {
        loginError = e.message;
      }
    }
  }
  
  function handleLoginSubmit(event: SubmitEvent) {
    event.preventDefault();
    const formData = {
      username: loginUsername,
      password: loginPassword
    };
    login(formData);
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-primary-500 p-4">
  <div class="bg-background-100 rounded-3xl p-6 w-full max-w-md border border-green-200">
    <!-- En-tête du formulaire -->
    <div class="text-center mb-10">
      <h1 class="text-4xl font-bold text-primary-600 mb-2 drop-shadow">
        Connexion
      </h1>
      <p class="text-primary-500 font-bold text-lg opacity-80">
        Connectez-vous à votre compte
      </p>
    </div>
    
    <!-- Formulaire de connexion -->
    <form onsubmit={handleLoginSubmit} class="space-y-6">
      <div class="space-y-2">
        <label for="login-username" class="block text-primary-600 font-semibold text-sm tracking-wide">
          Adresse email
        </label>
        <input
          id="login-username"
          bind:value={loginUsername}
          placeholder="nom d'utilisateur"
          class="w-full px-5 py-4 border-2 border-green-200 rounded-xl text-green-800 placeholder-gray-400 transition-all duration-300 focus:border-green-500 focus:ring-4 focus:ring-green-100 focus:outline-none focus:-translate-y-0.5 bg-white/80 focus:bg-white"
          required
        />
      </div>
      
      <div class="space-y-2">
        <label for="login-password" class="block text-primary-600 font-semibold text-sm tracking-wide">
          Mot de passe
        </label>
        <input
          id="login-password"
          type="password"
          bind:value={loginPassword}
          placeholder="••••••••"
          class="w-full px-5 py-4 border-2 border-green-200 rounded-xl text-green-800 placeholder-gray-400 transition-all duration-300 focus:border-green-500 focus:ring-4 focus:ring-green-100 focus:outline-none focus:-translate-y-0.5 bg-white/80 focus:bg-white"
          required
        />
      </div>
      
      <button 
        type="submit" 
        class="w-full bg-primary-500 text-white py-5 px-8 rounded-xl font-semibold text-lg uppercase tracking-wider transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-green-500/40 active:translate-y-0 mt-8"
      >
        Se connecter
      </button>
      
      <div class="text-center pt-6">
        <p class="text-green-700">
          Pas encore de compte ?
          <button 
            type="button" 
            onclick={() => goto("/register")} 
            class="text-green-500 font-semibold underline hover:text-green-800 transition-colors ml-1"
          >
            S'inscrire
          </button>
        </p>
      </div>
    </form>
  </div>
</div>
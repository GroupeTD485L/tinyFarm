package com.example.tinyfarm.controller;


import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Value("${my_github.pat}")
    private String githubToken;

    @PostMapping("/github")
    public ResponseEntity<?> loginWithGitHub(@RequestBody Map<String, String> payload) {
        String code = payload.get("code");

        // Si on détecte un mode test, on renvoie un jeton GitHub prédéfini
        if ("test-mode".equals(code)) {
            return ResponseEntity.ok(Map.of(
                "access_token", githubToken, // Utilisation du PAT GitHub
                "token_type", "bearer"
            ));
        }

        // Sinon, on suit le flow OAuth normal
        return fetchGitHubAccessToken(code);
    }

    private ResponseEntity<?> fetchGitHubAccessToken(String code) {
        // Normalement ici, on effectue un appel HTTP à l'API OAuth de GitHub
        return ResponseEntity.ok(Map.of(
            "access_token", "REAL_OAUTH_TOKEN", // Simulé ici
            "token_type", "bearer"
        ));
    }
}

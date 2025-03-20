package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.authgithub.service.UserService;

import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;

import java.util.Map;

@RestController
@PreAuthorize("isAuthenticated()")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/user")
    public Map<String, Object> user(Authentication authentication) {
        return Map.of(
            "username", userService.getUsername(authentication),
            "roles", userService.getRoles(authentication)
        );
   }

    @GetMapping("/admin")
    @PreAuthorize("hasRole('ADMIN')") // ✅ Seuls les admins OAuth peuvent accéder
    public Map<String, Object> adminOnly() {
        return Map.of("message", "Admin endpoint accessible");
    }
}

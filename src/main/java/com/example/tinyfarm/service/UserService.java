package com.example.tinyfarm.service;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class UserService {

    public String getUsername(Authentication authentication) {
        if (authentication == null) {
            throw new RuntimeException("Authentication is null");
        }

        if (authentication.getPrincipal() instanceof OAuth2User) {
            OAuth2User oauthUser = (OAuth2User) authentication.getPrincipal();
            return oauthUser.getAttribute("login"); // GitHub OAuth2
        } else if (authentication instanceof JwtAuthenticationToken) {
            return authentication.getName(); // JWT -> "sub"
        } else {
            throw new RuntimeException("Unsupported authentication type: " + authentication.getClass().getSimpleName());
        }
    }

    public List<String> getRoles(Authentication authentication) {
        if (authentication == null) {
            throw new RuntimeException("Authentication is null");
        }

        return authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .collect(Collectors.toList());
    }
}

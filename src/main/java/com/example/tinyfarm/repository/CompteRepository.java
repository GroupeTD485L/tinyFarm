package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Compte;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface CompteRepository extends JpaRepository<Compte, Long> {
    // Page<Compte> findAll(Pageable pageable);  // Ajout de la pagination
    // Page<Compte> findAllByFarm(Ferme ferme, Pageable pageable);
    Optional<Compte> findByPseudo(String pseudo);
}

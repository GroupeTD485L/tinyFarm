package com.example.tinyfarm.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import  com.example.tinyfarm.entity.Compte;

public interface CompteRepository extends JpaRepository<Compte, String> {
    Page<Compte> findAll(Pageable pageable);  // Ajout de la pagination
    Page<Compte> findAllByFarm(Ferme ferme, Pageable pageable);
}

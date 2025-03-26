package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Compte;
import  com.example.tinyfarm.entity.Ferme;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;


public interface CompteRepository extends JpaRepository<Compte, String> {
    // Page<Compte> findAll(Pageable pageable);  // Ajout de la pagination
    // Page<Compte> findAllByFarm(Ferme ferme, Pageable pageable);
}

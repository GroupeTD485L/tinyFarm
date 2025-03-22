package com.example.tinyfarm.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import  com.example.tinyfarm.entity.Poule;

public interface PouleRepository extends JpaRepository<Poule, String> {
    Page<Poule> findAll(Pageable pageable);  // Ajout de la pagination
    Page<Poule> findAllByFarm(Ferme ferme, Pageable pageable);
}

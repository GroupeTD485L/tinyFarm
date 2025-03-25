package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Poule;
import  com.example.tinyfarm.entity.Ferme;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface PouleRepository extends JpaRepository<Poule, String> {
    Page<Poule> findAll(Pageable pageable);  // Ajout de la pagination
    Page<Poule> findAllByFarm(Ferme ferme, Pageable pageable);
}

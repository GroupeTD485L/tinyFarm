package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Classement;
import  com.example.tinyfarm.entity.Ferme;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;


public interface ClassementRepository extends JpaRepository<Classement, Long> {
    // Page<Classement> findAll(Pageable pageable);  // Ajout de la pagination
    // Page<Classement> findAllByFarm(Ferme ferme, Pageable pageable);
}

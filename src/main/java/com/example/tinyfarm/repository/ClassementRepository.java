package com.example.tinyfarm.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import  com.example.tinyfarm.entity.Classement;

public interface ClassementRepository extends JpaRepository<Classement, String> {
    Page<Classement> findAll(Pageable pageable);  // Ajout de la pagination
    Page<Classement> findAllByFarm(Ferme ferme, Pageable pageable);
}

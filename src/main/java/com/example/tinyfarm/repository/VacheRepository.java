package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Vache;
import  com.example.chicken.entity.Ferme;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface VacheRepository extends JpaRepository<Vache, String> {
    Page<Vache> findAll(Pageable pageable);  // Ajout de la pagination
    Page<Vache> findAllByFarm(Ferme ferme, Pageable pageable);
}

package com.example.tinyfarm.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import  com.example.tinyfarm.entity.Vache;

public interface VacheRepository extends JpaRepository<Vache, String> {
    Page<Vache> findAll(Pageable pageable);  // Ajout de la pagination
    Page<Vache> findAllByFarm(Ferme ferme, Pageable pageable);
}

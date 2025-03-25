package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Commerce;
import  com.example.tinyfarm.entity.Ferme;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;


public interface CommerceRepository extends JpaRepository<Commerce, String> {
    Page<Commerce> findAll(Pageable pageable);  // Ajout de la pagination
    Page<Commerce> findAllByFarm(Ferme ferme, Pageable pageable);
}

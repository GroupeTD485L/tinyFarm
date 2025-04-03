package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Vache;
import com.example.tinyfarm.entity.Ferme;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;



public interface VacheRepository extends JpaRepository<Vache, Long> {
    Vache findByProprietaire(Ferme proprietaire);
    Page<Vache> findAll(Pageable pageable);
}

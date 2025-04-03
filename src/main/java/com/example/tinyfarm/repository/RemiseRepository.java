package com.example.tinyfarm.repository;
import java.util.List;
import java.util.Optional;
import  com.example.tinyfarm.entity.Remise;
import  com.example.tinyfarm.entity.Ferme;
import  com.example.tinyfarm.entity.Produit;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;


public interface RemiseRepository extends JpaRepository<Remise, Long> {
    Page<Remise> findAll(Pageable pageable);  // Ajout de la pagination
    Page<Remise> findAllByProprietaire(Ferme ferme, Pageable pageable);
    Optional<Remise> findByIdProduitAndProprietaire(Produit produit,Ferme ferme); // trouve la remise avec le produit qu'on veut
    Optional<Remise> findById(Long idRemise);
    List<Remise> findByProprietaire(Ferme ferme);
    Optional<Remise> findByProprietaireAndIdProduit(Ferme ferme,Produit produit); 
}

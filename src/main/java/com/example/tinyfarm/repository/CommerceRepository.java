package com.example.tinyfarm.repository;

import com.example.tinyfarm.entity.*;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.Query;

import java.util.Optional;

public interface CommerceRepository extends JpaRepository<Commerce, Long> {
    Page<Commerce> findAll(Pageable pageable);  // Ajout de la pagination
    Page<Commerce> findAllByVendeur(Ferme ferme, Pageable pageable);
    Page<Commerce> findAllByProduit(Produit produit, Pageable pageable);
    Page<Commerce> findAllByProduitOrderByPrixUnitaireAsc(Produit produit, Pageable pageable);
    
    long countByProduitAndAcheteurIsNotNull(Produit produit);
    long countByProduitAndVendeurAndAcheteurIsNotNull(Produit produit, Ferme vendeur);
    Optional<Commerce> findById(Long id);

    @Query("SELECT AVG(c.prixUnitaire) FROM Commerce c WHERE c.produit.idProduit = :id AND c.acheteur IS NULL")
    Double findAveragePriceById(long id);
}

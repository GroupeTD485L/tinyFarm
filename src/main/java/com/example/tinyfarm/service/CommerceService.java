package com.example.tinyfarm.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.Duration;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;

import com.example.tinyfarm.entity.*;
import com.example.tinyfarm.repository.CommerceRepository;
import com.example.tinyfarm.repository.FermeRepository;
import com.example.tinyfarm.repository.ProduitRepository;
import com.example.tinyfarm.repository.RemiseRepository;

import java.util.Optional;

@Service
public class CommerceService {
    private final CommerceRepository commerceRepository;
    private final FermeRepository fermeRepository;
    private final ProduitRepository produitRepository;
    private final RemiseRepository remiseRepository;

    public CommerceService(
            CommerceRepository commerceRepository,
            FermeRepository fermeRepository,
            ProduitRepository produitRepository,
            RemiseRepository remiseRepository
        ) {
        this.commerceRepository = commerceRepository;
        this.fermeRepository = fermeRepository;
        this.produitRepository = produitRepository;
        this.remiseRepository = remiseRepository;
    }

    @Transactional
    public Commerce addComerce(Commerce commerce) {
        return commerceRepository.save(commerce);
    }

    @Transactional
    public Commerce addCommerce(Long idVendeur, Long idProduit, int quantite, float prixUnitaire) {
        Optional<Ferme> existingVendeur = fermeRepository.findById(idVendeur);
        Optional<Produit> existingProduit = produitRepository.findById(idProduit);

        if (!existingVendeur.isPresent()) {
            throw new IllegalArgumentException("Le vendeur " + idVendeur + " n'existe pas !");
        }
        
        if ( !existingProduit.isPresent()) {
            throw new IllegalArgumentException("Le produit " + idProduit + " n'existe pas !");
        }

        Ferme vendeur = existingVendeur.get();
        Produit produit = existingProduit.get();

        Commerce commerce = new Commerce();
        commerce.setVendeur(vendeur);
        commerce.setAcheteur(null);
        commerce.setProduit(produit);
        commerce.setQuantite(quantite);
        commerce.setPrixUnitaire(prixUnitaire);
        commerce.setDateAchat(LocalDateTime.now());

        return commerceRepository.save(commerce);
    }

    @Transactional
    public Commerce addOffre(Long idVendeur, Long idProduit, int quantite, float prixUnitaire)
    {
        Optional<Ferme> existingVendeur = fermeRepository.findById(idVendeur);
        Optional<Produit> existingProduit = produitRepository.findById(idProduit);

        if (!existingVendeur.isPresent()) {
            throw new IllegalArgumentException("Le vendeur " + idVendeur + " n'existe pas !");
        }
        
        if ( !existingProduit.isPresent()) {
            throw new IllegalArgumentException("Le produit " + idProduit + " n'existe pas !");
        }

        Ferme vendeur = existingVendeur.get();
        Produit produit = existingProduit.get();

        Optional<Remise> existingRemise = remiseRepository.findByIdProduitAndProprietaire(produit, vendeur);
        if (!existingRemise.isPresent()) {
            throw new IllegalArgumentException("Le joueur " + vendeur.getNom() + "n'a pas de " + produit.getNom());
        }
        Remise remise = existingRemise.get();

        if (quantite > remise.getQuantite()) {
            throw new IllegalArgumentException("Le joueur ne possède pas assez de " + produit.getNom());
        }

        remise.setQuantite(remise.getQuantite() - quantite);
        remiseRepository.save(remise);
        return addCommerce(idVendeur, idProduit, quantite, prixUnitaire);
    }

    @Transactional
    public void deleteCommerce(Long idCommerce) {
        Optional<Commerce> existingCommerce = commerceRepository.findById(idCommerce);
        if (existingCommerce.isPresent()) {
            commerceRepository.delete(existingCommerce.get());
        } else {
            throw new IllegalArgumentException("Le rang " + idCommerce + "n'existe pas !");
        }
    }
    
    // Permet de faire une transaction entre 2 joueurs
    @Transactional
    public void executeTransaction(Long idFerme, Long idProduit, int quantite) {
        // Vérification des paramètres
        Optional<Ferme> existingFerme = fermeRepository.findById(idFerme);
        Optional<Produit> existingProduit = produitRepository.findById(idProduit);

        if (!existingFerme.isPresent()) {
            throw new IllegalArgumentException("Le vendeur " + idFerme + " n'existe pas !");
        }
        
        if ( !existingProduit.isPresent()) {
            throw new IllegalArgumentException("Le produit " + idProduit + " n'existe pas !");
        }

        Ferme ferme = existingFerme.get();
        Produit produit = existingProduit.get();

        // Vérification des capacités d'achat
        float prixMoyen = commerceRepository.findAveragePriceByIdProduit(produit);

        if (prixMoyen * quantite > ferme.getEcus()) {
            throw new IllegalArgumentException("La ferme ne possède pas assez d'écus");
        }

        long totalProduitVente = commerceRepository.findTotalQuantityByProduit(produit);
        if (totalProduitVente < quantite) {
            throw new IllegalArgumentException("Pas assez de produit en vente");
        }

        // Transaction qui s'effectue
        int iPage = 0;
        while (quantite > 0) {
            Page<Commerce> commerces = commerceRepository.findAllByProduitOrderByPrixUnitaireAsc(produit, PageRequest.of(iPage, 10));
            
            for (Commerce commerce : commerces) {
                if (quantite <= 0) {
                    break;
                }

                Ferme vendeur = commerce.getVendeur();
                int qtDispo = commerce.getQuantite();
                // Cas où l'offre ne propose pas assez de produit
                if (qtDispo < quantite) {
                    float montantTransaction = prixMoyen * qtDispo;
                    // Application de la transaction
                    vendeur.setEcus(vendeur.getEcus() + montantTransaction);
                    ferme.setEcus(ferme.getEcus() - montantTransaction);
                    Optional<Remise> existingRemise = remiseRepository.findByIdProduitAndProprietaire(produit, ferme);
                    if (existingRemise.isPresent()) {
                        Remise remise = existingRemise.get();
                        remise.setQuantite(remise.getQuantite() + qtDispo);
                        remiseRepository.save(remise);
                    } else {
                        Remise remise = new Remise(ferme, produit, qtDispo);
                        remiseRepository.save(remise);
                    }
                    quantite -= qtDispo;
                    commerce.setAcheteur(ferme);
                    commerceRepository.save(commerce);
                } else { // Cas où l'offre a ce qu'il faut
                    float montantTransaction = prixMoyen * quantite;
                    vendeur.setEcus(vendeur.getEcus() + montantTransaction);
                    ferme.setEcus(ferme.getEcus() - montantTransaction);
                    commerce.setQuantite(qtDispo - quantite);
                    commerceRepository.save(commerce);
                    Optional<Remise> existingRemise = remiseRepository.findByIdProduitAndProprietaire(produit, ferme);
                    if (existingRemise.isPresent()) {
                        Remise remise = existingRemise.get();
                        remise.setQuantite(remise.getQuantite() + quantite);
                        remiseRepository.save(remise);
                    } else {
                        Remise remise = new Remise(ferme, produit, quantite);
                        remiseRepository.save(remise);
                    }
                    Commerce transac = new Commerce(ferme, vendeur, produit, quantite, commerce.getPrixUnitaire());
                    commerceRepository.save(transac);
                    quantite = 0;
                }
                fermeRepository.save(vendeur);
            }
            iPage++;
        }
        
        fermeRepository.save(ferme);
    }

    @Transactional
    public void updateCommerce(Long id) {
        int iPage = 0;
        Page<Commerce> commerces;

        do {
            commerces = commerceRepository.findAllByAcheteurIsNull(PageRequest.of(iPage, 10));

            for (Commerce commerce : commerces) {
                if (Duration.between(commerce.getDateAchat(), LocalDateTime.now()).toDays() >= 7) {
                    Optional<Remise> existingRemiseVendeur = remiseRepository.findByIdProduitAndProprietaire(commerce.getProduit(), commerce.getVendeur());
                    if (existingRemiseVendeur.isPresent()) {
                        Remise remiseVendeur = existingRemiseVendeur.get();
                        remiseVendeur.setQuantite(remiseVendeur.getQuantite() + commerce.getQuantite());
                        remiseRepository.save(remiseVendeur);
                    } else {
                        Remise remiseVendeur = new Remise(commerce.getVendeur(), commerce.getProduit(), commerce.getQuantite());
                        remiseRepository.save(remiseVendeur);
                    }
                    
                    commerceRepository.delete(commerce);
                }
            }

            iPage++;
        } while (!commerces.isEmpty());
    }
}
package com.example.tinyfarm.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.Duration;

import com.example.tinyfarm.entity.Produit;
import com.example.tinyfarm.entity.Commerce;
import com.example.tinyfarm.entity.Ferme;
import com.example.tinyfarm.repository.CommerceRepository;
import com.example.tinyfarm.repository.FermeRepository;
import com.example.tinyfarm.repository.ProduitRepository;

import java.util.Optional;

@Service
public class CommerceService {
    private final CommerceRepository commerceRepository;
    private final FermeRepository fermeRepository;
    private final ProduitRepository produitRepository;

    public CommerceService(
            CommerceRepository commerceRepository,
            FermeRepository fermeRepository,
            ProduitRepository produitRepository
        ) {
        this.commerceRepository = commerceRepository;
        this.fermeRepository = fermeRepository;
        this.produitRepository = produitRepository;
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
    public void deleteCommerce(Long idCommerce) {
        Optional<Commerce> existingCommerce = commerceRepository.findById(idCommerce);
        if (existingCommerce.isPresent()) {
            commerceRepository.delete(existingCommerce.get());
        } else {
            throw new IllegalArgumentException("Le rang " + idCommerce + "n'existe pas !");
        }
    }
    /*
    @Transactional
    public void executeTransaction(Long id, int quantite) {
        Optional<Commerce> existingCommerce = commerceRepository.findById(id);
        Commerce commerce = existingCommerce.get();
        Ferme vendeur = commerce.getVendeur();
        Ferme acheteur = commerce.getAcheteur();
        float prixMoyen = commerceRepository.findAveragePriceById(id);
        float montantTransaction = quantite*prixMoyen;
        List<Commerce> commerces = commerceRepository.findAllByProduitOrderByPrixAsc(ProduitService.findById(id));
        for (Commerce c : commerces) {
            if (c.getQuantite()<=quantite) {
                c.getVendeur().setEcus(c.getQuantite()*prixMoyen);
                quantite-=c.getQuantite();
                commerceRepository.deleteById(c.getIdTransac());
            } else if (c.getQuantite()>quantite) {
                c.setQuantite(c.getQuantite()-quantite);
                break;
            }
        }
        acheteur.setEcus(acheteur.getEcus()-montantTransaction);// On retire les écus à l'acheteur
        //TODO : Retirer les produits aux vendeurs et les donner à l'acheteur
        if (quantite == commerce.getQuantite()) {
            commerceRepository.deleteById(id);
        } 
    }

    @Transactional
    public void checkCommerce(Long id) {
        Optional<Commerce> existingCommerce = commerceRepository.findById(id);
        if (Duration.between(LocalDateTime.now(), existingCommerce.get().getDateAchat()).toDays() >= 7) { // Si la date actuelle dépasse la date d'achat (qui est la date de création du commerce) + 7 jours, alors on supprime le commerce
            commerceRepository.deleteById(id);
            // TODO : Remettre les produits du commerce dans la réserve
        }
    }
    */
}
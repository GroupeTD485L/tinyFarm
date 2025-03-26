package com.example.tinyfarm.entity;
import java.time.LocalDateTime;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "classement")
public class Classement{
    @Id
    private Long idClassement;

    @OneToOne
    @MapsId
    @JoinColumn(name="idFerme", nullable = false)
    private Ferme ferme;

    private float score;

    public Classement(){}

    public Classement(float score){
        this.score = score;
    }
}
